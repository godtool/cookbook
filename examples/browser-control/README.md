# GRPO training with BrowserGym

https://github.com/huggingface/trl/blob/main/examples/scripts/openenv/browsergym.py

## BrowserGym Server Implementation

This example includes a comprehensive implementation plan for deploying the BrowserGym environment as a Modal server. See [BROWSER_GYM_SERVER.md](./BROWSER_GYM_SERVER.md) for the complete implementation plan.

### Key Features
- **Modal Cloud Deployment**: Run BrowserGym environment on Modal's serverless platform
- **External Access**: Expose the environment to external traffic for remote training
- **Docker Integration**: Use existing BrowserGym Docker images
- **GRPO Training**: Compatible with TRL's GRPOTrainer for reinforcement learning

### Quick Start
1. Set up Modal account and authentication
2. Deploy the BrowserGym server to Modal
3. Update client code to connect to remote environment
4. Run GRPO training with remote BrowserGym

## Environment setup

Installation instructions for `OpenEnv` are [here](https://meta-pytorch.org/OpenEnv/quickstart/)
```sh
git clone https://github.com/meta-pytorch/OpenEnv
uv pip install -e OpenEnv

# not sure if needed
uv openenv-core
```

```python
# Update import in file OpenEnv/src/envs/browsergym_env/client.py:
# from browsergym_env.models import (
#     BrowserGymAction,
#     BrowserGymObservation,
#     BrowserGymState,
# )
from .models import (
    BrowserGymAction,
    BrowserGymObservation,
    BrowserGymState,
)
```

Start Docker container with the RL environment:

```sh
docker login registry.hf.space -u Paulescu
Password: <PASTE_YOUR_HF_TOKEN_HERE>
```

```sh
docker run -p 8000:8000 \
  -e BROWSERGYM_BENCHMARK="miniwob" \
  -e BROWSERGYM_TASK_NAME="click-test" \
  registry.hf.space/burtenshaw-browsergym-env-95313e2:latest
```




