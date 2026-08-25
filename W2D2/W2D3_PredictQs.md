

Your final image size (code plus a CPU torch, no weights baked in): about 1000 MB.


If you COPY . . before installing requirements, how many of your next ten code edits will re-run pip install? all of them because it is in a layer before the install requirements layer


After a slim pass (right base, .dockerignore, no pip cache), the image will shrink from 8000 MB to 1000 MB. because we have pytorch and cuda install




python:3.11-slim alone is roughly how many MB? (check: docker pull python:3.11-slim && docker images python:3.11-slim) 130 mb


A naive single-stage build that COPYs the whole repo (including .git, docs, your virtualenv if you have one locally) before installing -- roughly how much bigger than the base image do you expect it to be?


A clean multi-stage build should get close to (base image) + (just your three dependencies: fastapi, uvicorn, pydantic). Estimate that total in MB.
