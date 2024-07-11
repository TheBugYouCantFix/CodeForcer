export async function uploadHandlesFile(file) {
  const url = `/students/file`;

  const response = await fetch(url, {
    method: "POST",
    body: file,
  });

  return response;
}
export async function uploadSingleHandle(info) {
  const url = `/students/${info.email}`;

  const response = await fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(info),
  });

  if (!response.ok) {
    console.error(response);
    throw new Error("Something went wrong");
  }

  return response;
}
