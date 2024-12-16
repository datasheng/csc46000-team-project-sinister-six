"use client";
import Visualization from "./Visualization";

const visPairs = [
  {
    vooID: "viz1734388284656",
    vooName: "VOOTimeseries",
    vooStaticImageURL:
      "https://public.tableau.com/static/images/VO/VOOTimeseries/VOOTimeseries/1.png",
    rspID: "viz1734388462258",
    rspName: "RSPTimeseries",
    rspStaticImageURL:
      "https://public.tableau.com/static/images/RS/RSPTimeseries/RSPTimeseries/1.png",
    conclusion:
      "Timeseries analysis shows trends in VOO and RSP over time for comparison.",
  },
  {
    vooID: "viz1734388471931",
    vooName: "VOOLinearRegression",
    vooStaticImageURL:
      "https://public.tableau.com/static/images/VO/VOOLinearRegression/VOOLinearRegression/1.png",
    rspID: "viz1734388478256",
    rspName: "RSPLinearRegression",
    rspStaticImageURL:
      "https://public.tableau.com/static/images/RS/RSPLinearRegression/RSPLinearRegression/1.png",
    conclusion:
      "Linear regression highlights patterns and correlations between VOO and RSP.",
  },
  {
    vooID: "viz1734388484843",
    vooName: "VOOVolumeByDate",
    vooStaticImageURL:
      "https://public.tableau.com/static/images/VO/VOOVolumeByDate/VOOVolumeByDate/1.png",
    rspID: "viz1734388491291",
    rspName: "RSPVolumeByDate",
    rspStaticImageURL:
      "https://public.tableau.com/static/images/RS/RSPVolumeByDate/RSPVolumebyDate/1.png",
    conclusion:
      "Volume analysis shows trading activity over time for VOO and RSP.",
  },
  {
    vooID: "viz1734388515832",
    vooName: "VOO7DayMovingAverage",
    vooStaticImageURL:
      "https://public.tableau.com/static/images/VO/VOO7DayMovingAvg/VOO7DayMovingAverage/1.png",
    rspID: "viz1734388522142",
    rspName: "RSP7DayMovingAverage",
    rspStaticImageURL:
      "https://public.tableau.com/static/images/RS/RSP7DayMovingAvg/RSP7DayMovingAverage/1.png",
    conclusion:
      "The 7-day moving average smooths short-term fluctuations in VOO and RSP.",
  },
  {
    vooID: "viz1734388527432",
    vooName: "VOO30DayMovingAverage",
    vooStaticImageURL:
      "https://public.tableau.com/static/images/VO/VOO30DayMovingAvg/VOO30DayMovingAverage/1.png",
    rspID: "viz1734388531686",
    rspName: "RSP30DayMovingAverage",
    rspStaticImageURL:
      "https://public.tableau.com/static/images/RS/RSP30DayMovingAvg/RSP30DayMovingAverage/1.png",
    conclusion:
      "The 30-day moving average highlights longer-term trends and patterns in VOO and RSP.",
  },
  {
    vooID: "viz1734388581615",
    vooName: "VOOvsRSPTimeseries",
    vooStaticImageURL:
      "https://public.tableau.com/static/images/VO/VOOvsRSPTimeseries/VOOvsRSPTimeseries/1.png",
    rspID: "",
    rspName: "",
    rspStaticImageURL: "",
    conclusion: "VOO vs RSP combined timeseries comparison.",
  },
];

const combinedVis = [
  {
    id: "viz1734388581615",
    name: "VOOvsRSPTimeseries",
    url: "https://public.tableau.com/static/images/VO/VOOvsRSPTimeseries/VOOvsRSPTimeseries/1.png",
    conclusion:
      "Combined timeseries analysis shows trends in VOO and RSP side by side for comparison.",
  },
];

export default function Home() {
  return (
    <div className="bg-primaryDark min-h-screen text-primaryLight flex flex-col text-center pt-10">
      <h1 className="text-6xl font-extrabold">Comparing Two ETFs</h1>
      <div className="flex-row flex justify-center text-4xl gap-8 pt-6 font-bold">
        <div className="border-2 border-primaryAccent rounded-3xl px-10 py-1">
          VOO
        </div>
        <div>vs</div>
        <div className="border-2 border-primaryAccent rounded-3xl px-10 py-1">
          RSP
        </div>
      </div>

      <div className="border-b border-primaryAccent w-3/5 mx-auto pt-10"></div>

      <div className="flex justify-center gap-8 p-8">
        <div className="flex flex-col gap-16">
          {visPairs.map((visPair) => (
            <div key={visPair.vooID} className="flex flex-col">
              <div className="flex">
                <div className="rounded-lg p-4 w-full">
                  <Visualization
                    id={visPair.vooID}
                    name={visPair.vooName}
                    staticImageUrl={visPair.vooStaticImageURL}
                  />
                </div>
                <div className="rounded-lg p-4 w-full">
                  <Visualization
                    id={visPair.rspID}
                    name={visPair.rspName}
                    staticImageUrl={visPair.rspStaticImageURL}
                  />
                </div>
              </div>
              <h2 className="text-4xl font-bold border-b border-gray-600 pb-4">
                {visPair.conclusion}
              </h2>
            </div>
          ))}

          {combinedVis.map((vis) => (
            <div key={vis.id} className="flex flex-col">
              <div className="rounded-lg p-4 w-full flex justify-center">
                <Visualization
                  id={vis.id}
                  name={vis.name}
                  staticImageUrl={vis.url}
                />
              </div>
              <h2 className="text-4xl font-bold border-b border-gray-600 pb-4">
                {vis.conclusion}
              </h2>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
