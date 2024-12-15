import { useEffect, useRef } from "react";

interface VisualizationProps {
  id: string;
  name: string;
  staticImageUrl: string;
  hostUrl?: string;
  toolbar?: "yes" | "no";
  tabs?: "yes" | "no";
}

const Visualization: React.FC<VisualizationProps> = ({
  id,
  name,
  staticImageUrl,
  hostUrl = "https://public.tableau.com/",
  toolbar = "yes",
  tabs = "no",
}) => {
  const vizContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (vizContainerRef.current) {
      const vizElement =
        vizContainerRef.current.getElementsByTagName("object")[0];
      vizElement.style.width = "800px";
      vizElement.style.height = "600px";

      const scriptElement = document.createElement("script");
      scriptElement.src = `${hostUrl}javascripts/api/viz_v1.js`;
      vizElement.parentNode?.insertBefore(scriptElement, vizElement);
    }
  }, [hostUrl]);

  return (
    <div
      className="tableauPlaceholder"
      id={id}
      style={{ position: "relative" }}
      ref={vizContainerRef}
    >
      <noscript>
        <a href="#">
          <img
            alt="Tableau Visualization"
            src={staticImageUrl}
            style={{ border: "none" }}
          />
        </a>
      </noscript>
      <object className="tableauViz" style={{ display: "none" }}>
        <param name="host_url" value={encodeURIComponent(hostUrl)} />
        <param name="embed_code_version" value="3" />
        <param name="site_root" value="" />
        <param name="name" value={name} />
        <param name="tabs" value={tabs} />
        <param name="toolbar" value={toolbar} />
        <param name="static_image" value={staticImageUrl} />
        <param name="animate_transition" value="yes" />
        <param name="display_static_image" value="yes" />
        <param name="display_spinner" value="yes" />
        <param name="display_overlay" value="yes" />
        <param name="display_count" value="yes" />
        <param name="language" value="en-US" />
      </object>
    </div>
  );
};

export default Visualization;
