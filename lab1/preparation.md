## Step 1: build docker images
1. enter into the `bootnode` path, e.g., `cd ./bootnode/`
2. run `sudo docker build -t bootnode .` to build the `bootnode` image
3. enter into the `node` path, e.g., `cd ./node/`
4. run `sudo docker build -t node .` to build the `node` image
5. run `sudo docker image ps` to check the images, the terminal will output the following information
   