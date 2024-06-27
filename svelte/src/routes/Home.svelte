<script>
    import { replace } from "svelte-spa-router";
    import Nav from './navigate.svelte';

    function log_out(){
     replace('/logout');  
    }
    function profile(){
     replace('/profile');  
    }
    
</script>
<Nav />
<h1>HOME PAGE</h1>
<div id = "log"><button on:click={log_out}>LOGOUT</button>  <button on:click={profile}>Profile</button></div>
<style>
h1{
    text-align: center;
}
#log{
    position: fixed; 
    top: 20px; 
    right: 20px; 
    padding: 10px 20px
}
</style>