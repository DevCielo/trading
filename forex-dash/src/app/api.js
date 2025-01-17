import axios from 'axios';

axios.defaults.baseURL = process.env.REACT_APP_API_URL;

const response = (resp) => resp.data;

const requests = {
    get: (url) => axios.get(url).then(response)
}

const endPoints = {
    account: () => requests.get('/account'),
    headlines: () => requests.get('/headlines'),
    technicals: (p, g) => requests.get(`/technicals/${p}/${g}`),
    prices: (p, g, c) => requests.get(`/prices/${p}/${g}/${c}`)
}

export default endPoints;