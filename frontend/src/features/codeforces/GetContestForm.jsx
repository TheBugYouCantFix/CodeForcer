import { useForm } from "react-hook-form";
import { useLocalStorageState } from "../../hooks/useLocalStorage.js";
import Form from "../../ui/Form.jsx";
import Input from "../../ui/Input.jsx";
import FormElement from "../../ui/FormElement.jsx";
import Button from "../../ui/Button.jsx";
import { useNavigate, useNavigation } from "react-router-dom";
import SpinnerMini from "../../ui/SpinnnerMini.jsx";

function GetContestForm() {
  const [id, setId] = useLocalStorageState("", "id");
  const [api, setApi] = useLocalStorageState("", "api");
  const [secret, setSecret] = useLocalStorageState("", "secret");
  const navigate = useNavigate();
  const navigation = useNavigation();

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

    navigate(`${contestID}`);
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <FormElement label="Contest URL" error={errors?.contestID?.message}>
        <Input
          placeholder="ID or full link"
          disabled={navigation.state !== "idle"}
          {...register("contestID", { required: "This field is required" })}
        />
      </FormElement>
      <FormElement
        label="Codeforces API"
        disabled={navigation.state !== "idle"}
        error={errors?.APIKey?.message || errors?.secretKey?.message}
      >
        <Input
          placeholder="API Key"
          disabled={navigation.state !== "idle"}
          {...register("APIKey", { required: "These fields are required" })}
        />
        <Input
          placeholder={"Secret Key"}
          disabled={navigation.state !== "idle"}
          {...register("secretKey", {
            required: "These fields are required",
          })}
        />
      </FormElement>
      <Button disabled={navigation.state !== "idle"} type="submit">
        {navigation.state !== "idle" ? <SpinnerMini /> : "Submit"}
      </Button>
    </Form>
  );
}

export default GetContestForm;
