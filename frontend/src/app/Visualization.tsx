import { useEffect } from "react";

declare global {
  namespace JSX {
    interface IntrinsicElements {
      "tableau-viz": React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & {
          src?: string;
          width?: string;
          height?: string;
          "hide-tabs"?: string;
          toolbar?: "top" | "bottom";
        },
        HTMLElement
      >;
    }
  }
}

interface VizualizationProps {
  src: string;
  width?: string;
  height?: string;
  hideTabs?: boolean;
  toolbar?: "top" | "bottom";
}

const Visualization: React.FC<VizualizationProps> = ({
  src,
  width = "800px",
  height = "500px",
  hideTabs = false,
  toolbar = "bottom",
}) => {
  useEffect(() => {
    const script = document.createElement("script");
    script.src =
      "https://us-east-1.online.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js";
    script.type = "module";
    script.async = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return (
    <div>
      <tableau-viz
        id="tableau-viz"
        src={src}
        width={width}
        height={height}
        hide-tabs={hideTabs.toString()}
        toolbar={toolbar}
      ></tableau-viz>
    </div>
  );
};

export default Visualization;
