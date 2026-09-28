"use client";

import { useEffect, useState } from "react";

type GraphicItem = {
  file: File;
  preview: string;
  width: number;
  x: number;
  y: number;
};

export default function Home() {
  const [name, setName] = useState("");
  const [title, setTitle] = useState("");

  const [logo, setLogo] = useState<File | null>(null);
  const [logoPreview, setLogoPreview] = useState("");

  const [graphics, setGraphics] = useState<GraphicItem[]>([]);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!logo) {
      setLogoPreview("");
      return;
    }

    const url = URL.createObjectURL(logo);

    setLogoPreview(url);

    return () => URL.revokeObjectURL(url);
  }, [logo]);

  function updateGraphic(
    index: number,
    field: "width" | "x" | "y",
    value: number
  ) {
    setGraphics((prev) =>
      prev.map((graphic, i) => {
        if (i !== index) return graphic;

        return {
          ...graphic,
          [field]: value,
        };
      })
    );
  }

  async function handleGenerate() {
    try {
      setLoading(true);

      const formData = new FormData();

      formData.append("name", name);
      formData.append("title", title);

      if (logo) {
        formData.append("logo", logo);
      }

      graphics.forEach((graphic) => {
        formData.append("graphics", graphic.file);
      });

      formData.append(
        "graphics_config",
        JSON.stringify(
          graphics.map((graphic) => ({
            width: graphic.width,
            x: graphic.x,
            y: graphic.y,
          }))
        )
      );

      const response = await fetch(
        "http://localhost:8000/generate",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Generation failed");
      }

      const blob = await response.blob();

      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");

      a.href = url;
      a.download = `${name || "nameplate"}.stl`;

      document.body.appendChild(a);
      a.click();
      a.remove();

      URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert("Failed to generate STL.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-5xl font-bold mb-2">
          Customized Nameplate Generator
        </h1>

        <p className="text-slate-400 mb-8">
          Create custom nameplates. Nameplates are 264mm x 64mm x 1.5mm.
        </p>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* LEFT PANEL */}

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <div className="space-y-6">
              <div>
                <label className="block mb-2">
                  Name
                </label>

                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="John Smith"
                  className="
                    w-full
                    bg-slate-800
                    border
                    border-slate-700
                    rounded-lg
                    px-4
                    py-3
                  "
                />
              </div>

              <div>
                <label className="block mb-2">
                  Title
                </label>

                <input
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Senior Systems Engineer"
                  className="
                    w-full
                    bg-slate-800
                    border
                    border-slate-700
                    rounded-lg
                    px-4
                    py-3
                  "
                />
              </div>

              {/* LOGO */}

              <div className="border border-slate-700 rounded-xl p-4">
                <label className="block mb-3 font-medium">
                  Company Logo
                </label>

                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) =>
                    setLogo(
                      e.target.files?.[0] || null
                    )
                  }
                />


               <p className="mt-4 text-xs text-green-400">
                  Logo loaded
                </p> 
              
              </div>

              {/* GRAPHICS */}

              <div className="border border-slate-700 rounded-xl p-4">
                <label className="block mb-3 font-medium">
                  Additional Graphics
                </label>

                <input
                  type="file"
                  multiple
                  accept="image/*"
                  onChange={(e) => {
                    if (!e.target.files) return;

                    const files = Array.from(
                      e.target.files
                    );

                    const mapped = files.map(
                      (file) => ({
                        file,
                        preview:
                          URL.createObjectURL(file),
                        width: 45,
                        x: 65,
                        y: 10,
                      })
                    );

                    setGraphics(mapped);
                  }}
                />

                <div className="space-y-4 mt-6">
                  {graphics.map((graphic, index) => (
                    <div
                      key={index}
                      className="
                        border
                        border-slate-700
                        rounded-xl
                        p-4
                      "
                    >
                      <div className="flex gap-4">
                        {graphic.preview}

                        <div className="flex-1">
                          <p className="font-semibold mb-3">
                            {graphic.file.name}
                          </p>

                          <div className="mb-3">
                            <label className="block text-sm">
                              Width ({graphic.width})
                            </label>

                            <input
                              type="range"
                              min="20"
                              max="80"
                              value={graphic.width}
                              onChange={(e) =>
                                updateGraphic(
                                  index,
                                  "width",
                                  Number(e.target.value)
                                )
                              }
                              className="w-full"
                            />
                          </div>

                          <div className="mb-3">
                            <label className="block text-sm">
                              X Position ({graphic.x})
                            </label>

                            <input
                              type="range"
                              min="-100"
                              max="100"
                              value={graphic.x}
                              onChange={(e) =>
                                updateGraphic(
                                  index,
                                  "x",
                                  Number(e.target.value)
                                )
                              }
                              className="w-full"
                            />
                          </div>

                          <div>
                            <label className="block text-sm">
                              Y Position ({graphic.y})
                            </label>

                            <input
                              type="range"
                              min="-50"
                              max="50"
                              value={graphic.y}
                              onChange={(e) =>
                                updateGraphic(
                                  index,
                                  "y",
                                  Number(e.target.value)
                                )
                              }
                              className="w-full"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <button
                onClick={handleGenerate}
                disabled={loading}
                className="
                  w-full
                  bg-blue-600
                  hover:bg-blue-500
                  rounded-xl
                  py-4
                  font-bold
                  disabled:bg-slate-700
                "
              >
                {loading
                  ? "Generating STL..."
                  : "Generate STL"}
              </button>
            </div>
          </div>

          {/* RIGHT PANEL */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

          <h2 className="text-xl font-semibold mb-4">
            Live Preview
          </h2>

          <div
            className="
              relative
              h-[160px]
              max-w-[640px]
              mx-auto
              rounded-xl
              bg-slate-700
              border
              border-slate-600
              overflow-hidden
            "
          >

            <div
              className="
                absolute
                top-4
                right-4
                w-20
                h-20
                border
                border-slate-500
                flex
                items-center
                justify-center
                text-xs
              "
            >
              LOGO
            </div>

            <div
              className="
                absolute
                left-1/2
                top-[55%]
                -translate-x-1/2
                text-xl
                font-bold
              "
            >
              {name || "NAME"}
            </div>

            <div
              className="
                absolute
                left-1/2
                top-[70%]
                -translate-x-1/2
                text-sm
              "
            >
              {title || "TITLE"}
            </div>

            {graphics.map((graphic, index) => (

              <div
                key={index}
                className="
                  absolute
                  bg-blue-500
                  rounded
                  flex
                  items-center
                  justify-center
                  text-xs
                  text-white
                "
                style={{
                  width: `${graphic.width}px`,
                  height: `${graphic.width}px`,
                  left: `${150 + graphic.x}px`,
                  top: `${60 + graphic.y}px`
                }}
              >
                G{index + 1}
              </div>

            ))}

          </div>
          </div>
        </div>
      </div>
    </main>
  );
}







