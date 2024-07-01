<script>
    import { replace } from "svelte-spa-router";
    import Nav from './navigate.svelte';
    function create(){
        replace('/createp');
    }
    function update(){
        replace('/updatep');
    }
</script>
<Nav /><br>
<h1>what do you want to do ?</h1><br>
<button on:click={create}>create product</button><br>
<button on:click={update}>update product</button><br>