<svelte:head>
	<script src="/static/pong/sources/main.js" type="module"></script>
	<link rel="stylesheet" href="/static/pong/style/style.css">
</svelte:head>

<!-- <script src="pong/sources/main.js" type="module"></script>
<script src="pong/sources/websocket/server_api.js" type="module"></script>
<script src="pong/sources/websocket/server_api_handler.js" type="module"></script>
<script src="pong/sources/websocket/objects_state.js" type="module"></script>
<script src="pong/sources/ui/overlay.js" type="module"></script>
<script src="pong/sources/ui/info.js" type="module"></script>
<script src="pong/sources/events/key_listener.js" type="module"></script>
<script src="pong/sources/events/resize.js" type="module"></script>
<script src="pong/sources/utils/class_vec.js" type="module"></script>
<script src="pong/sources/utils/data_origin.js" type="module"></script>
<script src="pong/sources/utils/game_type.js" type="module"></script>
<script src="pong/sources/utils/constants_objects.js" type="module"></script>
<script src="pong/sources/utils/defines.js" type="module"></script>
<script src="pong/sources/utils/debug.js" type="module"></script>
<script src="pong/sources/utils/cookie.js" type="module"></script>
<script src="pong/sources/utils/timer.js" type="module"></script>
<script src="pong/sources/collisions/collision.js" type="module"></script>
<script src="pong/sources/collisions/collision_utils.js" type="module"></script>
<script src="pong/sources/objects/class_game.js" type="module"></script>
<script src="pong/sources/objects/class_ball.js" type="module"></script>
<script src="pong/sources/objects/class_vertex.js" type="module"></script>
<script src="pong/sources/objects/class_paddle.js" type="module"></script>
<script src="pong/sources/objects/class_mesh.js" type="module"></script>
<script src="pong/sources/objects/class_shader.js" type="module"></script> -->

<div class="wrapper h-100 position-relative">
	<canvas class="card border-2 mx-auto h-100" id="glcanvas">
	</canvas>
	<div class="position-absolute top-0 start-50 translate-middle-x text-center">
		<div><span id="score"></span></div>
		<div><span id="time"></span></div>
	</div>
</div>