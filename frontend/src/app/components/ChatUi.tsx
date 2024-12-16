"use client";
import { useState, ChangeEvent } from "react";

type Msg = {
  author: string;
  message: string;
};

function ChatUi() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<Msg[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!query) return;

    setResponse((prev) => [
      ...prev,
      {
        author: "Me",
        message: query,
      },
    ]);

    setLoading(true);

    try {
      const res = await fetch(
        `http://127.0.0.1:5000/query_llm?query=${query}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      setQuery("");

      if (res.status !== 200) {
        console.log("There was an error while handling the request");
      }

      if (res.status === 200) {
        const data = await res.json();
        setResponse((prev) => [
          ...prev,
          {
            author: "LLM",
            message: data,
          },
        ]);
      }
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  };

  return (
    <div className="bg-primaryDark w-full h-[100vh] flex flex-col items-center justify-center">
      <h1 className="text-6xl font-extrabold">AI Chat</h1>
      <form
        className="pt-20 w-full flex-col flex items-center justify-center"
        onSubmit={handleSubmit}
      >
        <input
          className="focus:outline-none text-black w-[900px] p-3 rounded-full"
          placeholder="Enter chat"
          value={query}
          onChange={handleChange}
        />
        <div className="flex items-start justify-start flex-col w-[900px] ">
          {response.map((res) => {
            return (
              <h1 className="pt-6" key={res.message}>
                <span className="text-[20px]  font-bold underline">
                  {res.author}
                </span>
                : <span className="text-[20px]">{res.message}</span>
              </h1>
            );
          })}
        </div>
        <div className="pt-6">{loading && <h1>Loading...</h1>}</div>{" "}
      </form>
    </div>
  );
}

export default ChatUi;
