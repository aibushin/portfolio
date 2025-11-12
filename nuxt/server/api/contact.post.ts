export default defineEventHandler(async (event) => {
    const body = await readBody(event)
    // TODO: добавить валидацию/отправку в почту/Telegram/CRM
    console.log('[contact]', body)
    return { ok: true }
})
