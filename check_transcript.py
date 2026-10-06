import json
import sys
sys.stdout.reconfigure(encoding="utf-8")
transcript_path = "C:/Users/admin/.gemini/antigravity/brain/9bb30fd8-3ee2-43a0-b63e-6a06a95817ac/.system_generated/logs/transcript_full.jsonl"
for line in open(transcript_path, "r", encoding="utf-8"):
    try:
        data = json.loads(line)
        if data.get("type") == "USER_INPUT" or data.get("type") == "PLANNER_RESPONSE" or data.get("type") == "SUBAGENT_MESSAGE":
            content = data.get("content", "")
            if "แผน" in content or "อัพเกรด" in content or "upgrade" in content.lower():
                print(f"Step {data.get('step_index')}: {data.get('type')}")
                print(content[:500])
                print("-" * 50)
    except Exception as e:
        pass
