"""
Patch script: fixes _generate_with_groq to add token-budget guard,
and _regenerate_as_2d_only to catch 413 errors immediately.
"""
import re, sys

TARGET = r"services\ai_service.py"

with open(TARGET, encoding="utf-8") as f:
    src = f.read()

# ── PATCH 1: _generate_with_groq ────────────────────────────────────────────
OLD_GROQ = '''    def _generate_with_groq(self, prompt: str) -> Optional[str]:
        """Generate code using Groq API"""
        try:
            # Validate prompt is not empty
            if not prompt or not prompt.strip():
                self.logger.error("Empty prompt provided to Groq API")
                return None
            
            # Get system prompt and validate it too
            system_prompt = self._get_system_prompt()
            if not system_prompt or not system_prompt.strip():
                self.logger.error("Empty system prompt")
                system_prompt = "You are a FreeCAD Python code generator. Generate clean, functional FreeCAD Python code."
            
            response = self.client.chat.completions.create(
                model=self.config.groq.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user", 
                        "content": prompt.strip()
                    }
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                top_p=0.95,
                stop=None
            )
            
            if response and response.choices:
                return response.choices[0].message.content
            return None
            
        except Exception as e:
            self.logger.error(f"Groq generation failed: {e}")
            return None'''

NEW_GROQ = '''    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimate: ~4 chars per token on average."""
        return max(1, len(text) // 4)

    def _generate_with_groq(self, prompt: str) -> Optional[str]:
        """Generate code using Groq API with token-budget guard."""
        try:
            if not prompt or not prompt.strip():
                self.logger.error("Empty prompt provided to Groq API")
                return None

            system_prompt = self._get_system_prompt()
            if not system_prompt or not system_prompt.strip():
                self.logger.error("Empty system prompt")
                system_prompt = (
                    "You are a FreeCAD Python code generator. "
                    "Generate clean 2D Draft-only FreeCAD Python blueprints."
                )

            # ── Token budget guard ───────────────────────────────────────────
            # Groq free tier: 6000 TPM input limit is safest assumption.
            # We reserve 4000 tokens for the response, leaving 6000 for input.
            MAX_INPUT_TOKENS = 6000
            system_tokens = self._estimate_tokens(system_prompt)
            prompt_tokens  = self._estimate_tokens(prompt)
            total_input    = system_tokens + prompt_tokens

            if total_input > MAX_INPUT_TOKENS:
                self.logger.warning(
                    f"Combined prompt too large (~{total_input} tokens, limit {MAX_INPUT_TOKENS}). "
                    "Truncating user prompt to fit."
                )
                # Truncate user prompt to stay within budget
                available = MAX_INPUT_TOKENS - system_tokens
                max_chars = available * 4
                prompt = prompt[:max_chars] + "\\n\\n[...truncated to fit token limit]"
                self.logger.info(f"User prompt truncated to {len(prompt)} chars")

            response = self.client.chat.completions.create(
                model=self.config.groq.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": prompt.strip()},
                ],
                max_tokens=min(self.config.max_tokens, 6000),
                temperature=self.config.temperature,
                top_p=0.95,
                stop=None,
            )

            if response and response.choices:
                return response.choices[0].message.content
            return None

        except Exception as e:
            err = str(e)
            if "413" in err or "rate_limit" in err.lower() or "tokens" in err.lower():
                self.logger.warning(
                    f"Groq token/rate-limit error — skipping AI, using template. ({err[:120]})"
                )
            else:
                self.logger.error(f"Groq generation failed: {e}")
            return None'''

if OLD_GROQ.replace('\r\n', '\n') in src.replace('\r\n', '\n'):
    src = src.replace('\r\n', '\n')
    src = src.replace(OLD_GROQ.replace('\r\n', '\n'), NEW_GROQ)
    print("Patch 1 (token guard) applied via LF match")
elif OLD_GROQ in src:
    src = src.replace(OLD_GROQ, NEW_GROQ)
    print("Patch 1 (token guard) applied via exact match")
else:
    # fallback: simple function name search and splice
    start = src.find("    def _generate_with_groq(self, prompt: str) -> Optional[str]:")
    end   = src.find("\n    def _fix_common_issues", start)
    if start != -1 and end != -1:
        src = src[:start] + NEW_GROQ + "\n\n" + src[end:]
        print("Patch 1 (token guard) applied via splice")
    else:
        print("ERROR: Could not locate _generate_with_groq to patch", file=sys.stderr)
        sys.exit(1)

# ── PATCH 2: _regenerate_as_2d_only — catch 413 immediately ─────────────────
OLD_REGEN_EXCEPT = '''        except Exception as e:
            self.logger.error(f"Regeneration failed: {e} — using blueprint template")
            return self._build_blueprint_template(command)'''

NEW_REGEN_EXCEPT = '''        except Exception as e:
            err = str(e)
            if "413" in err or "rate_limit" in err.lower() or "tokens" in err.lower():
                self.logger.warning(
                    f"Rate/token limit during regeneration — using blueprint template. ({err[:120]})"
                )
            else:
                self.logger.error(f"Regeneration failed: {e} — using blueprint template")
            return self._build_blueprint_template(command)'''

if OLD_REGEN_EXCEPT in src:
    src = src.replace(OLD_REGEN_EXCEPT, NEW_REGEN_EXCEPT)
    print("Patch 2 (regen 413 handling) applied")
else:
    print("WARNING: Patch 2 target not found — skipping (non-fatal)")

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(src)

print(f"Successfully patched {TARGET}  ({len(src)} bytes)")
