<script>
    import { replace } from 'svelte-spa-router';
    let email = "";
    let otp = '';
    let dispaly="none";
    $:dispaly:dispaly
    let odispaly ='block';
    $:odispaly:odispaly
    
    let  pass ="";
  

    async function send_otp(){
        let formData = {
        email: email,
      };
        try{
    let response = await fetch(`http://127.0.0.1:8000/forget_password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      let data = await response.json();
      if(data.message  == "user not found"){
        alert(data.message);}
      else if(data.message == "Email sent successfully"){
        dispaly="block";
        odispaly='none';
      }  
      else{
        alert("not sent");
    }}
    catch (error) {
      console.error( error);
    }}

    async function send_pass(){
        let formData = {
        token : otp,
        new_password : pass
      };
        try{
    let response = await fetch(`http://127.0.0.1:8000/reset_password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      let data = await response.json();
      alert('pass changed!!')
      replace('/');
    }
    catch (error) {
      console.error( error);
    }
    }

</script>
<body>
  
<h1>please wait until the email recived in your account so that the otp and password form is available</h1>
<form>
    <table>
        <tr><th>enter your email :</th><th><input type="text" bind:value={email}></th></tr>
        <tr> <th colspan="2" align="right">
            <button on:click={send_otp}>send token</button>
        </th> </tr>
         </table>
</form>
<div style="display: {dispaly};">
<form>
    <table>
        <tr><th>otp :</th><input type="text" bind:value={otp}></tr>
        <tr><th>new password :</th><th><input type="text" bind:value={pass}></th></tr>
        <tr> <th colspan="2" align="right">
            <button on:click={send_pass}>save pass</button>
        </th> </tr>
    </table>
</form></div></body>
<style>
  body {
    overflow: auto;
    background: linear-gradient(to bottom, #d47d19, #a50b58);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}


h1 {
    text-align: center;
    color: #fff;
    text-decoration: underline;
    margin-bottom: 20px;
  }

  form {
    width: 80%;
    max-width: 600px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 8px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }

  th {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }

  th {
    background-color: #f2f2f2;
    font-weight: bold;
  }

  input[type="text"] {
    width: calc(100% - 20px); /* Adjusted to account for padding */
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
  }

button {
    padding: 10px 20px;
    background-color: rgb(182, 37, 134);
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
  }

  button:hover {
    background-color: #45a049;
  }


</style>