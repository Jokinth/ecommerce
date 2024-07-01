<script>
    import { replace } from "svelte-spa-router";

 let user = {
    user_name : "",
    email : "",
    password : "",
    mobile_number : "",
    role : ""
  };

let  address = {
    street : "",
    city : "",
    state : "",
    country : ""
  };

  function role_value(event){
    user.role = event.target.value;
  }
    async function submit(event){
        event.preventDefault();
        let formData = {
      user: {
        user_name: user.user_name,
        email: user.email,
        password: user.password,
        mobile_number: user.mobile_number,
        role: user.role
      },
      addresses: {
        street: address.street,
        city: address.city,
        state: address.state,
        country: address.country
      }
    };
        try {
      const response = await fetch('http://127.0.0.1:8000/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      localStorage.setItem('userID', data.user_id);
      //if(data.role == "u"){
      replace(`/home`);

    } catch (error) {
      console.error('Error signing up:', error);
    }
    }
</script>

<body style="text-align: center;">
    <h1 style="text-align:center"><b><u>USER SIGN UP</u></b></h1>
    <form on:submit={submit}>
        <table border="1" style="margin-left: auto; margin-right : auto;">
            <tr> <th>NAME :</th> <th> <input type = "text" bind:value = {user.user_name} required > </th> </tr>
            <tr> <th>E-MAIL ID : </th> <th> <input type = "email" bind:value={user.email} required> </th> </tr>
            <tr> <th>MOBILE NUMBER :</th> <th> <input type = "text" bind:value={user.mobile_number} required> </th> </tr>
            <tr> <th>PASSWORD :</th> <th> <input type = "password" bind:value={user.password} required> </th> </tr>
            <tr> <th>ROLE :</th> <th> <input type = "radio" name="role" value="user" on:change={role_value} required>USER 
                <input type = "radio" name="role" value="admin" on:change={role_value} >ADMIN </th> </tr>
            <tr><th colspan="2" align="left"><u><b>ADDRESS </b></u> </th></tr>
            <tr> <th> STREET :</th> <th> <input type = "text" bind:value={address.street} required> </th> </tr>
            <tr> <th> CITY :</th> <th> <input type = "text" bind:value={address.city} required> </th> </tr>
            <tr> <th> STATE :</th> <th> <input type = "text" bind:value={address.state} required> </th> </tr>
            <tr> <th> COUNTRY :</th> <th> <input type = "text" bind:value={address.country} required> </th> </tr>
            <tr> <th colspan="2" align="right">
                <input type="submit" value="Sign up">
            </th> </tr>
        </table>
    </form>
    <style>
        a{
            color: black;
            text-decoration: none;
        }
    </style>
</body>