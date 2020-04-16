import session from './session';
export default {
    getTable() {
        return session.get('/continent/');
        },
    };
