// 웹소켓 연결 설정
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export const useWebsocketStore = defineStore('websocket', () => {

  const socket = ref(null)
  let isRunning = true
  const authStore = useAuthStore()
  const stockCode = ref(null)
  const requestStr = ref(null)
  const processedData = ref(null)

  const webSocketStart = function (stockcode) {
    stockCode.value = stockcode
    
    requestStr.value = isNaN(stockcode) ? 'HDFSCNT0' : 'H0STCNT0' // 국외 : 국내
    socket.value = new WebSocket('ws://ops.koreainvestment.com:21000')

    socket.value.onopen = () => {
      console.log('WebSocket 연결이 열렸습니다.')
      dataFetchLoop()
    }
    
    socket.value.onerror = (error) => {
      console.error('WebSocket 오류:', error)
    }
    
    socket.value.onclose = () => {
      console.log('WebSocket 연결이 닫혔습니다.')
      isRunning = false
    }
  }

  // 입력 신호 보내기 

  const dataFetchLoop = async () => {
    sendMessage()
    while (isRunning) {
      await receiveMessage()
      await sleep(3000) // 3초 대기
    }
  }

  const sendMessage = () => {
    const newCode = isNaN(stockCode.value) ? `DNAS${stockCode.value}` : stockCode.value
    if (socket.value && socket.value.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify({
        header: {
          approval_key: authStore.websocketToken,
          custtype: "P",
          tr_type: "1",
          content_type: "utf-8"
        },
        body: {
          input: {
            tr_id: requestStr.value,
            tr_key: newCode
          }
        }
      }))
    }
  }

  const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))

  const receiveMessage = () => {
    return new Promise((resolve) => {
      socket.value.onmessage = (event) => {
        try {
          if (isNaN(stockCode.value)){
            // console.log(event)
            processedData.value = stockspurchaseUsa(event.data)
          }
          else {processedData.value = stockspurchaseDomestic(event.data)}
          resolve(processedData.value)
        } catch (error) {
          console.error('Data processing error:', error)
          resolve(null)
        }
      }
    })
  }

  // 미국 데이터 처리 함수
  const stockspurchaseUsa = (data) => {
    const pValue = data.split('^')
    const price = parseFloat(pValue[11])*(1,395.77)
    // 시간 문자열을 타임스탬프로 변환
    const timestamp = new Date().getTime() + (9 * 60 * 60 * 1000)
    console.log(timestamp, price)
    // NaN 체크 및 처리
    if (isNaN(price)) {
      console.warn('Invalid price value received:', pValue[11])
      return null // 유효하지 않은 데이터는 null 반환
    }
    
    return {
      timestamp: timestamp,
      price: price
    }
  }

  // 국내 데이터 처리 함수
  const stockspurchaseDomestic = (data) => {
    const pValue = data.split('^')
    const price = parseInt(pValue[2])
    // 현재 시간을 Date 객체로 변환
    const date = new Date(new Date().getTime())
    
    // HH:mm:ss 형식으로 포맷팅
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const seconds = String(date.getSeconds()).padStart(2, '0')
    const formattedTime = `${hours}${minutes}${seconds}`

    console.log(formattedTime, price)
    // NaN 체크 및 처리
    if (isNaN(price)) {
      console.warn('Invalid price value received:', pValue[2])
      return null // 유효하지 않은 데이터는 null 반환
    }
    
    return {
    time: formattedTime,
    price: price
    }
  }

  //   // 국내 데이터 처리 함수
  // const stockspurchaseDomestic = (data) => {
  //   const pValue = data.split('^')
  //   const price = parseInt(pValue[2])
  //   // 현재 시간을 Date 객체로 변환
  //   const date = new Date()

  //   // NaN 체크 및 처리
  //   if (isNaN(price)) {
  //     console.warn('Invalid price value received:', pValue[2])
  //     return null // 유효하지 않은 데이터는 null 반환
  //   }
    
  //   return {
  //   time: date.toISOString(),
  //   price: price
  //   }
  // }

return { webSocketStart, socket, processedData}
})
