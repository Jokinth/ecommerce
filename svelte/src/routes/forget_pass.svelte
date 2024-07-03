<script>
    import { replace } from 'svelte-spa-router';
    let email = "";
    let otp = '';
    let dispaly="none";
    $:dispaly:dispaly
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
<h1>please wait until the email recived in your account so that the otp and password form is available</h1>
<form>
    <table>
        <tr><th>enter your email :</th><th><input type="text" bind:value={email}></th></tr>
        <tr> <th colspan="2" align="right">
            <button on:click={send_otp}>send token</button>
        </th> </tr>
         </table>
</form>
<form>
    <table>
        <div style="display: {dispaly};"><tr><th>otp :</th><input type="text" bind:value={otp}></tr>
        <tr><th>new password :</th><th><input type="text" bind:value={pass}></th></tr>
        <tr> <th colspan="2" align="right">
            <button on:click={send_pass}>save pass</button>
        </th> </tr></div>
    </table>
</form>