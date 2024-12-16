"use client";
import { useState, ChangeEvent } from "react";

type Msg = {
  author: string;
  message: string;
};

function ChatUi() {
  const [query, setQuery] = useState<string>("");
  const [index, setIndex] = useState<string>("");
  const [getNews, setGetnews] = useState<boolean>(false);
  const [response, setResponse] = useState<Msg[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!query) return;
    if (getNews && index.length < 1) return;

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
        getNews
          ? `http://127.0.0.1:5000/query_llm?query=${query}`
          : `http://127.0.0.1:5000//query_llm_news?query=${query}index=${index}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      setQuery("");
      setIndex("");

      if (res.status !== 200) {
        console.error("There was an error while handling the request");
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
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleNewsState = () => {
    // to remove the value before removeing it from the screen
    if (getNews) {
      setIndex("");
    }
    setGetnews((prev) => !prev);
  };

  return (
    <div className="bg-primaryDark w-full h-[100vh] flex flex-col items-center justify-center">
      <h1 className="text-6xl font-extrabold">AI Chat</h1>
      <button
        className="ml-5 w-[110px] h-[50px] rounded-lg text-white text-[20px] hover:opacity-50 underline"
        onClick={handleNewsState}
      >
        {getNews ? "News" : "Regular"}
      </button>
      <form
        className="pt-20 w-full flex-col flex items-center justify-center"
        onSubmit={handleSubmit}
      >
        <div>
          {getNews && (
            <input
              className="focus:outline-none text-black w-[120px] h-[55px] p-3 border border-black border-r-5   border-l-0 border-t-0 border-b-0"
              placeholder="Enter Index"
              value={index}
              onChange={(e: ChangeEvent<HTMLInputElement>) => {
                setIndex(e.target.value);
              }}
            />
          )}
          <input
            className="focus:outline-none text-black w-[800px] h-[55px] p-3"
            placeholder="Enter chat"
            value={query}
            onChange={(e: ChangeEvent<HTMLInputElement>) => {
              setQuery(e.target.value);
            }}
          />
          <button className="ml-5 w-[110px] h-[50px] bg-yellow-500 rounded-lg text-primaryDark">
            Enter
          </button>
        </div>
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
        <div className="pt-6">{loading && <h1>Loading...</h1>}</div>
      </form>
    </div>
  );
}

export default ChatUi;
