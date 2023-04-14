**[UNDER DEVELOPMENT CURRENTLY!!]**
<h1>P2P Chatroom</h1>

<br>
<p>This is a CLI-based p2p chatroom implemented in Python. The chatroom allows multiple peers to communicate with each other over the network without the need for a centralized server. Instead, the server is hosted on one of the peers in the chatroom, and if that peer goes offline, the server automatically gets hosted on another online peer in the chatroom with the best connectivity.</p> <p>This auto-hosting server here will be called as the <strong>Rendezvous</strong></p>

<h2>Requirements</h2>
<ul>
   <li>Python 3.x</li>
   <li><code>asyncio</code> library</li>
   <li><code>sockets</code> built-in python lib</li>
</ul>

<h2>Usage</h2>
<p>To start the chatroom, run the <code>server.py</code> script on one of the peers:</p>
<!-- ```python:
python server.py
``` -->
<div><code>python server.py</code></div>

<br>
<p>This will start the server and allow other peers to connect to it.</p>

<p>To connect to the chatroom from another peer, run the <code>client.py</code> script:</p>
<!-- ```python:
python client.py &lt;server_ip_address&gt;
``` -->
<div><code>python client.py &lt;server_ip_address&gt;</code></div>

<br>
<p>Replace <code>&lt;server_ip_address&gt;</code> with the IP address of the peer hosting the server.</p>

<p>Once connected, you can send messages to other peers in the chatroom using the following format:</p>
<!-- ```python:
@peer_name &lt;message&gt;
``` -->
<div><code>@peer_name &lt;message&gt;</code></div>

<br>
<p>Replace <code>&lt;peer_name&gt;</code> with the name of the peer you want to send the message to.</p>
<p>And remove <code>&lt;peer_name&gt;</code> if you want to send the message to the whole chatroom.</p>

<p>To quit the chatroom, type <code>exit</code> or <code>quit</code>.</p>

<h2>Implementation Details</h2>
<p>The chatroom is implemented using <code>asyncio</code> and uses a custom protocol for exchanging messages between peers. The server runs on one of the peers and listens for incoming connections. When a peer connects, it adds the peer to the chatroom and sends a list of all connected peers to the new peer.</p>
<p>Each peer maintains a list of all other peers in the chatroom and their connection status. When the server goes offline, the peer with the best connectivity automatically becomes the new server and starts hosting the chatroom.</p>

<h2>Security</h2>
<p>The chatroom does not currently implement any security measures and should not be used to exchange sensitive information. If you plan to use the chatroom in a production environment, you should consider implementing security measures such as authentication and encryption.</p>
<h2>License</h2>
<p>This project is licensed under the MIT License - see the <a href="LICENSE.md" target="_new">LICENSE.md</a> file for details.</p>
<h2>Acknowledgments</h2>
<ul>
   <li>Thanks to the <code>asyncio</code> team for providing such a powerful and flexible library for building network applications.</li>
   <li>Thanks to the open-source community for contributing to the development of Python and the many libraries that make projects like this possible.</li>
</ul>
