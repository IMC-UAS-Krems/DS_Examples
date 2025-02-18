# Setting up the p2p network

1. Create the docker image for the node

``docker build -t p2pnode:latest .``

2. Create a new bridge user network

``docker network create p2pnetwork``

3. Run the first node and connect to the network (detached in interacive mode)

``docker run -dit --network p2pnetwork --name node0 -p :7123 p2pnode:latest``

4. Find out IP address of node0 in the network

``docker network inspect p2pnetwork``

5. Run the next n containers passing the IP address of node0 as the env variable `P2P_REMOTE_HOST`

``docker run -dit --network p2pnetwork --name noden -p :7123 -e="P2P_REMOTE_HOST=172.21.0.2" p2pnode:latest``

6. Check the output of node1 to see if it joined the network successfully

``docker container logs node1``

7. Attach to node1 and add a (key, value) pair to the network

``docker attach node1``

8. Detach from node1 (escape sequence CTRL + p + q)

9. Check the logs of node0, node1, etc. to see that the key, value was stored