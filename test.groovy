apiVersion: v1
kind: Pod
metadata:
   name: test

spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
      - containerPort: 80
  
  - name: ubuntu
    image: ubuntu:latest
    ports:
      - containerPort: 88    

   