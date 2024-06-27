import Signup from './routes/signup.svelte';
import Login from './routes/login.svelte';
import Home from './routes/Home.svelte';
import Logout from './routes/logout.svelte';
import Profile from './routes/profile_edit.svelte';
import Edit_name from './routes/edit_name.svelte';
import Edit_email from './routes/edit_email.svelte';
import Edit_mobile from './routes/edit_mobile.svelte';
import Edit_pass from './routes/edit_pass.svelte';
import Add_address from './routes/address.svelte';
import Forget from './routes/forget_pass.svelte';
import Reset from './routes/reset_pass.svelte';

export const routes = {
    '/home': Home,
    '/':Login,
    '/signup': Signup,
    '/logout':Logout,
    '/profile':Profile,
    '/profile/edit_name':Edit_name,
    '/profile/edit_email':Edit_email,
    '/profile/edit_mobile':Edit_mobile,
    '/profile/edit_pass':Edit_pass,
    '/profile/add_address':Add_address,
    '/forget_pass':Forget,
    '/reset_pass':Reset,
};