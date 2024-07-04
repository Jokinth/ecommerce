<script>
    import { replace } from 'svelte-spa-router';
    import Nav from './navigate.svelte';
    let review_text= '';
    let review_rating='';
    let pid = localStorage.getItem('current_product');
    const token = localStorage.getItem('token');
    let review = [];
    let product = {
        pid: 0,
     quantity_available: 0,
     brand: "",
     pname: "",
     price: 0,
     category: "",
     description: ""
    } ;
    async function fetchProduct() {
    try {
      let response = await fetch(`http://127.0.0.1:8000/read_product/${pid}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      let data = await response.json();
      product = data;
    } catch (error) {
      console.error(error);
    }
  }
  fetchProduct();

  async function reviews() {
    try {
      let response = await fetch(`http://127.0.0.1:8000/read_reviews/${pid}`, {
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
      review = data;
    } catch (error) {
      console.error(error);
    }
  }
  reviews();
  async function  add_review(event){
    event.preventDefault();
        
        let formData = {
    rating: review_rating,
    review_text: review_text,
    };
        try {
      const response = await fetch(`http://127.0.0.1:8000/review/${pid}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      alert('review added');
      reviews();
    } catch (error) {
      console.error('Error signing up:', error);
    }
  }

function setRating(value) {
  review_rating = value;
}
</script>

<Nav />
<br>

<h1>name:{product.pname}</h1><br>
<h3>price:{product.price}</h3><br>
<h3>quantity available:{product.quantity_available}</h3><br>
<h3>description:{product.description}</h3><br>
<h3>category:{product.category}</h3><br>
<h3>brand:{product.brand}</h3><br>

<form on:submit={add_review}><input type="text" bind:value={review_text}>
  <div class="rating">
    rating:
    <input type="radio" id="star5" name="rating"  on:change={setRating(1)}  />
    ★
    <input type="radio" id="star4" name="rating"  on:change={setRating(2)}  />
    ★
    <input type="radio" id="star3" name="rating"  on:change={setRating(3)}  />
    ★
    <input type="radio" id="star2" name="rating"  on:change={setRating(4)}  />
    ★
    <input type="radio" id="star1" name="rating"  on:change={setRating(5)}  />
    ★
  </div>
  
<input type="submit" value="add review"></form>

<h1>reviews:</h1>
{#each review as r}
<h3> user : {r.username} rating : {r.rating} review : {r.review_text}  </h3>
{/each}
	

<!--[
  {
    "id": 1,
    "uid": 17,
    "rating": 5,
    "review_text": "spuer product",
    "pid": 15
  }
]-->


