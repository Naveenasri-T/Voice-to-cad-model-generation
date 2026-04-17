"""
Patch: Replace all 3D-generating prompt methods with a single clean 2D-only prompt method.
This eliminates 'import Part', 'Part::Box', and 3D instructions from the AI prompt entirely.
"""
import sys

TARGET = r"services\ai_service.py"

with open(TARGET, encoding="utf-8") as f:
    src = f.read()

# Normalise line endings for matching
src_lf = src.replace("\r\n", "\n")

# ── Find the block from _create_professional_prompt to _get_system_prompt ────
START_MARKER = "    def _create_professional_prompt(self, command: str, model_type: str, quality_level: str, include_materials: bool) -> str:"
END_MARKER   = "    def _get_system_prompt(self) -> str:"

start_idx = src_lf.find(START_MARKER)
end_idx   = src_lf.find(END_MARKER)

if start_idx == -1 or end_idx == -1:
    print(f"ERROR: markers not found (start={start_idx} end={end_idx})", file=sys.stderr)
    sys.exit(1)

print(f"Replacing lines from pos {start_idx} to {end_idx}")

REPLACEMENT = '''    def _create_professional_prompt(self, command: str, model_type: str = "2d",
                                    quality_level: str = "professional",
                                    include_materials: bool = False) -> str:
        """Create a concise 2D-only user prompt for the AI.

        The heavy structural rules live in the system prompt (ai_system_prompt.txt).
        This user prompt only needs to:
          1. State what to draw
          2. Remind the AI of the house layout and room names
          3. Stay SHORT to avoid exceeding Groq's 12000 TPM limit
        """
        cmd = (command or "2BHK house blueprint").strip()

        # Detect number of bedrooms from command
        bhk = "2"
        for n in ["1", "2", "3", "4"]:
            if f"{n}bhk" in cmd.lower() or f"{n} bhk" in cmd.lower():
                bhk = n
                break

        room_map = {
            "1": "Living Room, Kitchen, Bedroom, Bathroom",
            "2": "Living Room, Dining, Master Bedroom, Bedroom 2, Kitchen, Bathroom, Toilet",
            "3": "Living Room, Dining, Master Bedroom, Bedroom 2, Bedroom 3, Kitchen, Bathroom 1, Bathroom 2, Store",
            "4": "Living Room, Dining, Master Bedroom, Bedroom 2, Bedroom 3, Bedroom 4, Kitchen, Dining, Study, Bathroom 1, Bathroom 2, Store",
        }
        rooms = room_map.get(bhk, room_map["2"])

        return (
            f"Draw a professional {bhk}BHK house architectural blueprint for: {cmd}\\n\\n"
            f"Rooms required: {rooms}\\n\\n"
            "Follow the system prompt structure exactly:\\n"
            "  1. Floor plan (y=0): exterior room_box(0,0,10500,8500,3.5), "
            "interior walls, door arcs, window symbols, furniture, room labels\\n"
            "  2. Front elevation (y=16000): facade, openings, parapet\\n"
            "  3. Side elevation (y=32000): depth profile, section hatching\\n"
            "  4. Grid (light grey columns A-J, rows 1-12, every 1200mm)\\n"
            "  5. Title block at bottom\\n\\n"
            "REMEMBER: Draft-only (no Part module), all Z=0, "
            ">=30 primitives, >=8 dim(), >=8 lbl()."
        )

'''

new_src = src_lf[:start_idx] + REPLACEMENT + "\n" + src_lf[end_idx:]

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(new_src)

print(f"Successfully patched {TARGET}  ({len(new_src)} bytes)")
print(f"  Removed {end_idx - start_idx} chars of 3D prompt code")
print(f"  Added   {len(REPLACEMENT)} chars of 2D-only prompt code")
