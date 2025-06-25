import axios from "axios";


const api = axios.create({ baseURL: process.env.API });

export { axios, api };
