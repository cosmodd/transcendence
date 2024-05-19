<script lang="ts">
    let visible: boolean = false;
    let message: string = "";
    let link: string = "/game/online";
  
    function handleNotification(e) {
      const det = e.detail;
      message = "Join the game!";
      visible = true;
  
      setTimeout(() => {
        visible = false;
      }, 30000);
    }
  
    const joinGame = () => {
      visible = false;
      window.location.href = link;
    };
  </script>
  
  <svelte:window on:notification={handleNotification} />
  
  {#if visible}
    <div class="toast show position-fixed bottom-0 end-0 p-3" style="z-index: 11">
      <div class="toast-header">
        <strong class="me-auto">Notification</strong>
        <button type="button" class="btn-close" on:click={() => (visible = false)}></button>
      </div>
      <div class="toast-body">
        {message}
        <div class="mt-2 pt-2 border-top">
          <button type="button" class="btn btn-primary btn-sm" on:click={joinGame}>Join Game</button>
        </div>
      </div>
    </div>
  {/if}
  