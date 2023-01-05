## Step 1: build docker images
1. enter into the `bootnode` path, e.g., `cd ./bootnode/`
2. run `sudo docker build -t bootnode .` to build the `bootnode` image
3. enter into the `node` path, e.g., `cd ./node/`
4. run `sudo docker build -t node .` to build the `node` image
5. run `sudo docker image ps` to check the images, the terminal will output contents like the following information
   ```sh
   REPOSITORY           TAG       IMAGE ID       CREATED          SIZE
   node                 latest    3fa445ef9361   6 seconds ago    384MB
   bootnode             latest    a5c759aa8ae6   48 seconds ago   384MB
   ethereum/client-go   v1.6.6    18a3fff827f9   5 years ago      384MB
   ```