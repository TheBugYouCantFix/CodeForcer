import { useForm } from "react-hook-form";
import { useState } from "react";
import SumbissionInfo from "../../ui/SumbissionInfo.jsx";
import { useLocalStorageState } from "../../hooks/useLocalStorage.js";
import Form from "../../ui/Form.jsx";
import Input from "../../ui/Input.jsx";
import FormElement from "../../ui/FormElement.jsx";
import Button from "../../ui/Button.jsx";
import SpinnerMini from "../../ui/SpinnnerMini.jsx";
import toast from "react-hot-toast";

function GetContestForm() {
  const [contestInfo, setContestInfo] = useState({});
  const [id, setId] = useLocalStorageState("", "id");
  const [api, setApi] = useLocalStorageState("", "api");
  const [secret, setSecret] = useLocalStorageState("", "secret");

  const [isGetting, setIsGetting] = useState(false);
  async function getContest(url) {
    setIsGetting(true);
    const response = await fetch(url, {
      // mode: "no-cors",
    });
    console.log(response);
    if (response.status >= 500) {
      throw new Error("Something went wrong with CodeForces");
    }
    if (!response.ok) {
      throw new Error("Something went wrong!");
    }

    const data = response.json();
    return data;
  }

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      contestID: id,
      APIKey: api,
      secretKey: secret,
    },
  });

  const onSubmit = function (data) {
    // Getting values from form
    let { contestID, APIKey, secretKey } = data;
    // Convert URL to id
    if (contestID.startsWith("http")) {
      contestID = contestID.slice(contestID.lastIndexOf("/") + 1);
    }
    // Setting values in local storage
    setId(contestID);
    setApi(APIKey);
    setSecret(secretKey);

    // Sendind GET request
    // `https://13bd4039-c465-4f54-b961-30824dc7cc9b.mock.pstmn.io/contests/52`
    const url = `http://10.90.137.106:8000/contests/${contestID}?key=${APIKey}&secret=${secretKey}`;
    getContest(url)
      .then((data) => {
        setContestInfo(data);
        setIsGetting(false);
      })
      .catch((err) => {
        toast.error(err.message);
        setIsGetting(false);
      });
  };

  return (
    <>
      {Object.keys(contestInfo).length === 0 && (
        <Form onSubmit={handleSubmit(onSubmit)}>
          <FormElement label="Contest URL" error={errors?.contestID?.message}>
            <Input
              placeholder="ID or full link"
              disabled={isGetting}
              {...register("contestID", { required: "This field is required" })}
            />
          </FormElement>
          <FormElement
            label="Codeforces API"
            error={errors?.APIKey?.message || errors?.secretKey?.message}
          >
            <Input
              placeholder="API Key"
              disabled={isGetting}
              {...register("APIKey", { required: "These fields are required" })}
            />
            <Input
              placeholder={"Secret Key"}
              disabled={isGetting}
              {...register("secretKey", {
                required: "These fields are required",
              })}
            />
          </FormElement>
          <Button disabled={isGetting} type="submit">
            {isGetting ? <SpinnerMini /> : "Submit"}
          </Button>
        </Form>
      )}

      {Object.keys(contestInfo).length !== 0 && (
        <SumbissionInfo info={contestInfo} reset={setContestInfo} />
      )}
    </>
  );
}

export default GetContestForm;
