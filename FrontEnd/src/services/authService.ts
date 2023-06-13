// eslint-disable-next-line import/no-extraneous-dependencies
import jwt_decode from 'jwt-decode';
import { login } from 'apis/user.api';

class AuthService {
  handleAuthentication = () => {
    const accessToken = this.getAccessToken();
    if (!accessToken) return;
    this.setSession('accessToken', accessToken);
  };

  loginWithToken = async (username: string, password: string) => {
    const loginResp = await login('/users/login', {
      username: username,
      password: password,
    });
    this.setSession('accessToken', loginResp.accessToken);
    const userStringify = JSON.stringify(loginResp);
    this.setSession('user', userStringify);
    return {
      fullName: loginResp.full_name,
      user: loginResp,
      role: loginResp.role || 'staff',
    };
  };

  setSession = (key: string, accessToken: string) => {
    localStorage.setItem(key, accessToken);
  };

  logOut = () => {
    localStorage.clear();
  };

  getUser = () => {
    const user = localStorage.getItem('user') || '';
    return user;
  };

  getAccessToken = () => localStorage.getItem('accessToken');

  isAuthenticated = () => {
    const token = this.getAccessToken();
    if (token) {
      try {
        const decodedToken: any = jwt_decode(token);
        if (typeof decodedToken === 'object' && decodedToken.exp) {
          const expirationTime = decodedToken.exp * 1000; // Convert to milliseconds
          const currentTime = Date.now();
          if (currentTime < expirationTime) {
            // Token is not expired
            return true;
          }
        }
      } catch (error) {
        // Token verification failed
        return false;
      }
    }
    return false;
  };

  //   isValidToken = (accessToken: string | null) => {
  //     const expireTime = 1606275140.897;
  //     if (!accessToken) return false;

  //     const currentTime = Date.now() / 1000;

  //     return expireTime < currentTime;
  //   };
}

const authService = new AuthService();

export default authService;
