// 웹소켓 연결 설정
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export const useWebsocketStore = defineStore('websocket', () => {

  const socket = ref(null)
  let isRunning = true
  const authStore = useAuthStore()
  const stockCode = ref(null)

  const webSocketStart = function (stockcode) {
    stockCode.value = stockcode
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
            tr_id: "H0STCNT0",
            tr_key: stockCode
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
          const processedData = stockspurchaseDomestic(event.data)
          if (processedData) { // null이 아닐 때만 처리
            updateChartData(processedData)
            console.log('Processed Data:', processedData)
          }
          resolve(processedData)
        } catch (error) {
          console.error('Data processing error:', error)
          resolve(null)
        }
      }
    })
  }

  const stockspurchaseDomestic = (data) => {
    console.log(data)
    const pValue = data.split('^')
    const price = parseInt(pValue[2])
    // 시간 문자열을 타임스탬프로 변환
    const timestamp = new Date().getTime() + (9 * 60 * 60 * 1000)
    // NaN 체크 및 처리
    if (isNaN(price)) {
      console.warn('Invalid price value received:', pValue[2])
      return null // 유효하지 않은 데이터는 null 반환
    }
    
    return {
      timestamp: timestamp,
      price: price
    }
  }

return { webSocketStart }
})
