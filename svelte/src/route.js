import Signup from './routes/signup.svelte';
import Login from './routes/login.svelte';
import Home from './routes/Home.svelte';
import Logout from './routes/logout.svelte';
import Profile from './routes/profile_edit.svelte';
import Add_address from './routes/address.svelte';
import Forget from './routes/forget_pass.svelte';
import Edit from './routes/edit.svelte';
import Product from './routes/product.svelte';
import Product_c from './routes/createp.svelte';
import Product_u from './routes/updatep.svelte';
import Product_up from './routes/update_product.svelte';

export const routes = {
    '/home': Home,
    '/':Login,
    '/signup': Signup,
    '/logout':Logout,
    '/profile':Profile,
    '/add_address':Add_address,
    '/forget_pass':Forget,
    '/product':Product,
    '/updatep':Product_u,
    '/createp':Product_c,
    '/edit':Edit,
    '/update_product':Product_up,
};