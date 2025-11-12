export const useAuth = () => {
    // accessToken теперь берём из cookie
    const accessToken = useCookie<string | null>("access_token", {
        sameSite: "lax",
        secure: false
    })
    return { accessToken }
}
