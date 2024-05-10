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
    fetch('http://localhost:8000/chat', {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
    .then((response) => response.json()) // 응답을 JSON으로 파싱
    .then((data) => {
      console.log("응답:", data); // 응답 데이터를 콘솔에 출력
      setMessage(data.answer); // 응답 데이터를 상태에 저장
    })
    .catch((error) => console.log("에러:", error));
    
  }
  console.log(watch("question"))
 
  return (
    <div className="h-screen flex justify-center items-center bg-gray-100">
      <div className="w-full max-w-4xl bg-white rounded-lg shadow-lg">
        <div className="p-8">
          <h2 className="text-4xl font-bold mb-8 text-center">Chat GPT</h2>
          <div className="bg-gray-200 rounded-lg p-6 mb-8 h-80 overflow-y-auto">
          {<h4>{message? message : ""}</h4>}
          </div>
          <form onSubmit={handleSubmit(onSubmit)}>
            <div className="flex items-center mb-6">
              <input
                type="text"
                {...register("question", { required: true })}
                className="flex-1 py-4 px-6 border border-gray-300 rounded-l-lg focus:outline-none focus:border-blue-500"
                placeholder="메시지를 입력하세요..."
              />
              <button
                type="submit"
                className="py-4 px-8 bg-blue-500 text-white font-bold rounded-r-lg transition duration-300 ease-in-out hover:bg-blue-600"
              >
                전송
              </button>
            </div>
            {errors.question && (
              <span className="text-red-500 block mb-4">메시지를 입력하세요.</span>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}