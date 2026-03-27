import json
import os
import sys

def main():
    config_path = "config.json"
    resolved_path = "config.resolved.json"
    workspace_path = "workspace"

    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found")
        sys.exit(1)

    with open(config_path, "r") as f:
        config = json.load(f)

    # 1. Update Providers
    if "providers" not in config:
        config["providers"] = {}
    if "custom" not in config["providers"]:
        config["providers"]["custom"] = {}
    
    config["providers"]["custom"]["apiKey"] = os.environ.get("LLM_API_KEY", config["providers"]["custom"].get("apiKey", ""))
    config["providers"]["custom"]["apiBase"] = os.environ.get("LLM_API_BASE_URL", config["providers"]["custom"].get("apiBase", ""))

    # 2. Update Agents Defaults
    if "agents" not in config:
        config["agents"] = {}
    if "defaults" not in config["agents"]:
        config["agents"]["defaults"] = {}
    
    config["agents"]["defaults"]["model"] = os.environ.get("LLM_API_MODEL", config["agents"]["defaults"].get("model", ""))

    # 3. Update MCP Tool Env
    if "tools" in config and "mcpServers" in config["tools"] and "lms" in config["tools"]["mcpServers"]:
        lms_config = config["tools"]["mcpServers"]["lms"]
        if "env" not in lms_config:
            lms_config["env"] = {}
        lms_config["env"]["NANOBOT_LMS_BACKEND_URL"] = os.environ.get("NANOBOT_LMS_BACKEND_URL", lms_config["env"].get("NANOBOT_LMS_BACKEND_URL", ""))
        lms_config["env"]["NANOBOT_LMS_API_KEY"] = os.environ.get("NANOBOT_LMS_API_KEY", lms_config["env"].get("NANOBOT_LMS_API_KEY", ""))
        lms_config["env"]["NANOBOT_VICTORIALOGS_URL"] = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428")
        lms_config["env"]["NANOBOT_VICTORIATRACES_URL"] = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428")

    # 4. Update Gateway
    if "gateway" not in config:
        config["gateway"] = {}
    config["gateway"]["host"] = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
    config["gateway"]["port"] = int(os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "8000"))

    # 5. Update Channels (Webchat)
    if "channels" not in config:
        config["channels"] = {}
    if "webchat" not in config["channels"]:
        config["channels"]["webchat"] = {}
    
    config["channels"]["webchat"]["enabled"] = True
    config["channels"]["webchat"]["host"] = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    config["channels"]["webchat"]["port"] = int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8001"))
    config["channels"]["webchat"]["access_key"] = os.environ.get("NANOBOT_ACCESS_KEY", "")
    config["channels"]["webchat"]["allow_from"] = ["*"]

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Config resolved to {resolved_path}")
    print(f"Starting nanobot gateway with workspace {workspace_path}...")

    # Launch nanobot gateway
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_path, "--workspace", workspace_path])

if __name__ == "__main__":
    main()
