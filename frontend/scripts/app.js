import { router } from './router.js';

window.addEventListener('popstate', router);
router();
