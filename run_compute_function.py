"""Polaris Compute Example


# Apptainer def file "polaris-apptainer-example.def"
Bootstrap: docker
From: python:3.12-slim

%post
    pip install --no-cache-dir globus-compute-endpoint globus-compute-sdk globus-sdk

%runscript
    exec python3 "$@"

# Build and run the Apptainer container to test.
apptainer build ~/polaris-apptainer-example.sif polaris-apptainer-example.def
apptainer exec ~/polaris-apptainer-example.sif \
  python3 -c "import globus_compute_sdk, globus_compute_endpoint; print(globus_compute_sdk.__version__)"
  
"""

from globus_compute_sdk import Executor
from globus_compute_sdk.serialize import ComputeSerializer, AllCodeStrategies

# Crux endpoint for Polaris Compute
endpoint_id = "fd8b54bb-9452-411d-8e3a-09408156a886"
# Polaris endpoint for Crux Compute (alternative)
# endpoint_id = "9a947ba5-f537-4681-acf3-cc66485aadec"


def hello():
    import globus_compute_sdk
    return f"Hello Globus Compute Version: ({globus_compute_sdk.__version__})"


def where_am_i():
    import os, socket
    marker = "/opt/container-marker.txt"
    return {
        "host": socket.gethostname(),
        "marker": open(marker).read().strip() if os.path.exists(marker) else None,
        "apptainer": os.environ.get("APPTAINER_CONTAINER"),
    }


serializer = ComputeSerializer(strategy_code=AllCodeStrategies())
gce = Executor(endpoint_id=endpoint_id,
               serializer=serializer,
               user_endpoint_config={"account": "APSDataAnalysis", 
                                     "queue": "debug",
                                     "container_type": "singularity",
                                     #  "container_image": "~/pytorch:22.06-py3.sing",
                                     "container_image": "~/polaris-apptainer-example.sif",
                                     })
future = gce.submit(where_am_i)
print(future.result())