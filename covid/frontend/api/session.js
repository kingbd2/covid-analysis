import axios from 'axios';

const protocol_result = location.protocol;
const slashes = protocol_result.concat('//');
const host = slashes.concat(window.location.hostname);
const host_with_port = host.concat(':8000');
const base_path = host_with_port.concat('/api/v1/');

const CSRF_COOKIE_NAME = 'csrftoken';
const CSRF_HEADER_NAME = 'X-CSRFToken';

const session = axios.create({
  headers: {
    "Content-Type": "application/json",
    // anything you want to add to the headers
  },
  withCredentials: true,
  timeout: 1000,
  xsrfCookieName: CSRF_COOKIE_NAME,
  xsrfHeaderName: CSRF_HEADER_NAME,
  baseURL: base_path,
});

export default session;
