# Docker build & push steps (screenshot each command + its output)

Replace `yourdockerhubusername` with your actual Docker Hub username throughout.

```bash
# 1. Log in to Docker Hub
docker login

# 2. Build the image (run from inside the app/ folder)
cd app
docker build -t yourdockerhubusername/traffic-monitoring:v1 .

# 3. Verify it locally
docker images | grep traffic-monitoring

# 4. Run it locally to confirm it works
docker run -d -p 5000:5000 --name traffic-test yourdockerhubusername/traffic-monitoring:v1
curl http://localhost:5000/
curl http://localhost:5000/intersections
docker logs traffic-test

# 5. Stop the test container
docker stop traffic-test && docker rm traffic-test

# 6. Push to Docker Hub
docker push yourdockerhubusername/traffic-monitoring:v1

# 7. (Optional but nice for the report) also tag and push :latest
docker tag yourdockerhubusername/traffic-monitoring:v1 yourdockerhubusername/traffic-monitoring:latest
docker push yourdockerhubusername/traffic-monitoring:latest
```

After step 6/7, visit `https://hub.docker.com/r/yourdockerhubusername/traffic-monitoring`
and screenshot the public repo page — that's your "publicly accessible, properly tagged" proof.