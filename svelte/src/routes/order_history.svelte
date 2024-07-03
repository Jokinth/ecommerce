<script>
    import Nav from './navigate.svelte';

    let currentUserID = localStorage.getItem('userID');
    let orders=[]
    async function fetch_orders() {
      try {
        let response = await fetch(`http://127.0.0.1:8000/read_order/${currentUserID}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        let data = await response.json();
        orders = data;
      } catch (error) {
        console.error(error);
      }
    }
fetch_orders();
</script>
<Nav/><br><br>

    <table border="1" style="width: 100%;">
      <thead>
        <tr>
          <th>order time</th>
          <th>address</th>
          <th>total amount</th>
        </tr>
      </thead>
      <tbody>
        {#each orders as order, i}
          <tr>
            <td>{order.order_time}</td>
            <td>{order.address}</td>
            <td>{order.total_amount}</td>
          </tr>  {/each}
        </tbody>
    </table>