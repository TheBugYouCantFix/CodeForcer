import Heading from "../ui/Heading.jsx";
import Form from "../ui/Form.jsx";
import Input from "../ui/Input.jsx";
import FileInput from "../ui/FileInput.jsx";
import FormElement from "../ui/FormElement.jsx";
import Button from "../ui/Button.jsx";
import { FaDatabase } from "react-icons/fa6";
import { useForm } from "react-hook-form";

function Handles() {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => console.log(data);
  console.log(watch("file"));

  return (
    <>
      <Heading as="h1">
        <FaDatabase />
        Edit Handles
      </Heading>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <FormElement label="File from Local Storage" type="file">
          <FileInput text="*.csv, *.xls, *.xlsx" {...register("file")} />
        </FormElement>
        <FormElement label="Link to Google Sheets">
          <Input
            placeholder="https://docs.google.com/spreadsheets/..."
            {...register("link")}
          />
        </FormElement>
        <input type="file" {...register("example")} />
        <Button as="input" type="submit" value="Submit" />
      </Form>
    </>
  );
}

export default Handles;
