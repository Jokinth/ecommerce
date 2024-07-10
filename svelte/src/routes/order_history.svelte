<script>
    import Nav from './navigate.svelte';

    let currentUserID = localStorage.getItem('userID');
    let orders=[];
    const token = localStorage.getItem('token');
    async function fetch_orders() {
      try {
        let response = await fetch(`http://127.0.0.1:8000/read_order`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
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
</script><div id='total'>
<Nav/><br><br>
<form>
    <table>
      <thead>
        <tr>
          <th>order</th>
          <th>order time</th>
          <th>address</th>
          <th>total amount</th>
        </tr>
      </thead>
      <tbody>
        {#each orders as order, i}
          <tr>
            <td>{i+1}</td>
            <td>{order.order_time}</td>
            <td>{order.address}</td>
            <td>{order.total_amount}</td>
          </tr>  {/each}
        </tbody>
    </table></form></div>
    <style>
      form {
    color:#010f01;
    margin: 20px auto;
    width: 1000px;
    padding: 20px;
    border: 1px solid #031103;
    border-radius: 5px;
    background-color: wheat;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  table {
    width: 100%;
    text-align: center;
  }
  #total{overflow: auto;
        background: linear-gradient(to bottom, #d47d19, #a50b58);
        height: 100vh; 
        display: flex;
        flex-direction: column;
    }
    </style>