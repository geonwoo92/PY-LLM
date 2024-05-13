"use client"
import React, { useState } from 'react';
import { useForm, SubmitHandler } from "react-hook-form";

type Message = {
  content: string;
  type: string;
}

type Inputs = {
  question: string;
}

export default function Home() {
  const [message, setMessage] = useState('')

  const { watch,register, handleSubmit, formState: { errors }, reset } = useForm<Inputs>();

  const onSubmit: SubmitHandler<Inputs> = (data) => {
    console.log('입력된 값 : ' + JSON.stringify(data));
    fetch('http://localhost:8000/api/chat/titanic', {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
    .then((response) => response.json()) // 응답을 JSON으로 파싱
    .then((data) => {
      console.log("응답:", data); // 응답 데이터를 콘솔에 출력
      setMessage(data); // 응답 데이터를 상태에 저장
    })
    .catch((error) => console.log("에러:", error));
    
  }
  // console.log(watch("question"))
 

  
  return (
  <>  <div className="h-screen flex justify-center items-center bg-gray-100">
  <div className="w-full h-full max-w-10xl bg-white rounded-lg shadow-lg">
    <div className="p-16">
      <div className="flex items-center justify-center">
        <h1 className="text-4xl font-bold">geon GPT에게 물어봐</h1>
      </div><br />
     
        <div className="grid grid-cols-3 gap-4 mb-4">
          <div className="border border-gray-300 p-4 rounded-lg">
            <label className="inline-flex items-center">
              <input type="radio" className="form-radio" name="radio" />
              <span className="ml-2">버튼1</span>
            </label>
            {/* 버튼1 아래에 사진이 들어갈 공간 */}
            <img src="/image/titanic.jpg" alt="Example" className="mt-4 w-full h-15 object-cover rounded-lg" />


          </div>
          <div className="border border-gray-300 p-4 rounded-lg">
            <label className="inline-flex items-center">
              <input type="radio" className="form-radio" name="radio" />
              <span className="ml-2">버튼2</span>
            </label>
            {/* 버튼2 아래에 사진이 들어갈 공간 */}
            <img src="/image/back.jpg" alt="Example" className="mt-4 w-full h-15 object-cover rounded-lg" />
          </div>
          <div className="border border-gray-300 p-4 rounded-lg">
            <label className="inline-flex items-center">
              <input type="radio" className="form-radio" name="radio" />
              <span className="ml-2">버튼3</span>
            </label>
            {/* 버튼3 아래에 사진이 들어갈 공간 */}
          </div>
        </div>
        <div className="bg-gray-200 rounded-lg p-4 mb-4 h-48 overflow-y-auto text-lg">
        <h4>{message ? message: "" }</h4>
      </div>
      <form onSubmit={handleSubmit(onSubmit)}>
        <input
          type="text"
          {...register("question", { required: true })}
          className="block w-full py-4 px-6 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:border-blue-500"
          placeholder="메시지를 입력하세요..."
        />
        <button
          type="submit"
          className="py-4 px-8 bg-blue-500 text-white font-bold rounded-lg transition duration-300 ease-in-out hover:bg-blue-600"
        >
          전송
        </button>
      </form>
    </div>
  </div>
</div>
</>)
}