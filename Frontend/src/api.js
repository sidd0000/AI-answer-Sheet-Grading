// src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5010/api', // your Flask port
});

export default api;
