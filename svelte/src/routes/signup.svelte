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
// Store the token and user information securely
localStorage.setItem('token', data.access_token);
localStorage.setItem('userID', data.user_ID);
localStorage.setItem('role', data.role);
localStorage.setItem('exp', data.exp);

      replace(`/home`);
    } catch (error) {
      console.error('Error signing up:', error);
    }
    }
</script>

<body style="text-align: center;">
    <h1 style="text-align:center"><b><u>USER SIGN UP</u></b></h1>
    <form on:submit={submit}>
        <table>
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
            <tr> <th colspan="2" id='submit'>
                <input type="submit" value="Sign up">
            </th> </tr>
        </table>
    </form>
  </body>
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
      padding: 8px;
      border-radius: 8px;
      background-color: wheat;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
   #submit{
    text-align: right;
   }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 20px;
    }
  
    th {
      padding: 8px;
      text-align: left;
      border-bottom: 1px solid #ddd;
      background-color: #f2f2f2;
      font-weight: bold;
    }
  
    input[type="text"] ,input[type="email"],input[type="password"]{
      width: calc(100% - 20px); 
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 14px;
    }
  
    input[type="submit"] {
      padding: 8px 20px;
      background-color: rgb(182, 37, 134);
      color: #fff;
      border: none;
      border-radius: 4px;
      text-align: right;
      cursor: pointer;
      font-size: 16px;
      transition: background-color 0.3s ease;
    }
  
    input[type="submit"]:hover {
      background-color: #45a049;
    }
    </style>