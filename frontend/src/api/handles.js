const uri = import.meta.env.VITE_API_URL;
export async function uploadHandlesFile(file) {
  const url = `${uri}/students/file`;

  const response = await fetch(url, {
    method: "POST",
    body: file,
  });

  return response;
}
export async function uploadSingleHandle(info) {
  const url = `${uri}/students`;

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(info),
  });

  if (!response.ok) {
    throw new Error("Something went wrong");
  }

  return response;
}
