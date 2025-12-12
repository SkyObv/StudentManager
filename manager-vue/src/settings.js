export default {
     Host: 'http://127.0.0.1:8000',          // 后端请求域名
     // 获取访问令牌
     getToken() {
         return localStorage.getItem('token') || sessionStorage.getItem('token')
     },
     // 获取刷新令牌
     getRefreshToken() {
         return localStorage.getItem('refresh_token') || sessionStorage.getItem('refresh_token')
     },
}