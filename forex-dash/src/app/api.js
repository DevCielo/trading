import axios from 'axios';

axios.defaults.baseURL = process.env.REACT_APP_API_URL;

const response = (resp) => resp.data;

const requests = {
    get: (url) => axios.get(url).then(response)
}

const endPoints = {
    account: () => requests.get('/account'),
    headlines: () => requests.get('/headlines')
}

export default endPoints;