import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { BsFillArrowLeftSquareFill } from "react-icons/bs";
import { useForm, Controller } from "react-hook-form";
import { handlePostRequest } from "../../api/contests.js";
import { useLocalStorageState } from "../../hooks/useLocalStorage.js";
import { Link, useNavigate } from "react-router-dom";
import Select from "react-select";

import {
  StyledCover,
  ButtonBack,
  Description,
  List,
  Item,
  ItemRow,
  ItemInput,
  Error,
  UndefinedDescription,
  LateSubmissionsContainer,
  TimeConfiguration,
  SubmissionsAction,
  SelectorDescription,
  SourcesDescription,
} from "./SubmissionsInfo.components.jsx";
import Button from "../../ui/Button.jsx";
import Heading from "../../ui/Heading.jsx";
import SpinnerMini from "../../ui/SpinnnerMini.jsx";
import FormElement from "../../ui/FormElement.jsx";
import Input from "../../ui/Input.jsx";
import FileInput from "../../ui/FileInput.jsx";

const selectStyles = {
  container: (baseStyles) => ({
    ...baseStyles,
    fontSize: "1.4rem",
    height: "4.5rem",
  }),
  control: (base) => ({
    ...base,
    height: "4.5rem",
  }),
};
const selectTheme = (theme) => ({
  ...theme,
  colors: {
    ...theme.colors,
    primary: "var(--color-brand-600)",
    primary75: "var(--color-brand-500)",
    primary50: "var(--color-brand-400)",
    primary25: "var(--color-brand-400)",
    danger: "var(--color-red-700)",
    dangerLight: "var(--color-red-100)",
    neutral0: "var(--color-grey-0)",
    neutral5: "var(--color-grey-50)",
    neutral10: "var(--color-grey-100)",
    neutral20: "var(--color-grey-200)",
    neutral30: "var(--color-grey-300)",
    neutral40: "var(--color-grey-400)",
    neutral50: "var(--color-grey-500)",
    neutral60: "var(--color-grey-600)",
    neutral70: "var(--color-grey-700)",
    neutral80: "var(--color-grey-800)",
    neutral90: "var(--color-grey-900)",
  },
});

function download(filename, text) {
  var element = document.createElement("a");
  element.setAttribute(
    "href",
    "data:text/plain;charset=utf-8," + encodeURIComponent(text),
  );
  element.setAttribute("download", filename);

  element.style.display = "none";
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

function SubmissionsInfo({ info, selectors, group }) {
  const { contest, participants } = info;
  const options = selectors?.map((el) => ({
    value: el?.name,
    label: el?.name?.slice(0, 1).toUpperCase() + el?.name?.slice(1),
    description: el?.description,
  }));
  const definedUsers = {
    ...contest,
    problems: contest.problems.map((item) => {
      return {
        ...item,
        submissions: item.submissions.filter(
          (item) => item.author.email != null,
        ),
      };
    }),
  };
  const undefinedUsers = participants
    .filter((el) => el?.email === null)
    .map((el) => el?.handle);
  const unpossibleReqest = undefinedUsers.length === participants.length;

  const navigate = useNavigate();

  const [contestInfo, setContestInfo] = useLocalStorageState(
    {},
    `contest-${contest.id}`,
  );

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    control,
    setError,
  } = useForm({
    defaultValues: {
      selector: options.find((el) => el?.value === "most points") || options[0],
    },
  });

  useEffect(() => {
    const subscription = watch((value) => {
      let totalPoints = 0;

      for (let key in value) {
        value[key] = parseFloat(value[key]);

        if (!isNaN(parseInt(key))) {
          totalPoints += parseFloat(value[key]);
        }
      }
      setContestInfo(value);

      if (totalPoints > 100) {
        setError("total", {
          type: "custom",
          message: "Total number of points must be less or equal to 100",
        });
      }
    });
    return () => subscription.unsubscribe();
  }, [setContestInfo, watch, setError]);

  const [isGetting, setIsGetting] = useState(false);
  const selectedValue = watch("selector");

  const onSubmit = function (data) {
    setIsGetting(true);

    handlePostRequest(definedUsers, data)
      .then((res) => {
        res
          .filter((el) => el !== undefined)
          .forEach((el) => {
            let filename = el?.headers
              ?.get("content-disposition")
              ?.match(/(?<=")(?:\\.|[^"\\])*(?=")/);
            filename = filename ? filename[0] : `CodeForcer-${Date.now()}`;
            el.blob().then((blob) => {
              const url = window.URL.createObjectURL(
                new Blob([blob], { type: blob.type }),
              );
              const link = document.createElement("a");
              link.href = url;
              link.setAttribute("download", filename);

              document.body.appendChild(link);
              link.click();
              link.parentNode.removeChild(link);
            });
          });
      })
      .catch((err) => toast.error(err.message))
      .finally(setIsGetting(false));
  };

  return (
    <StyledCover>
      <ButtonBack onClick={() => navigate("/contests")}>
        <BsFillArrowLeftSquareFill />
      </ButtonBack>
      <Heading as="h2">Contest &quot;{contest.name}&quot;</Heading>
      <Description>
        Total number of problems: {contest.problems.length}
      </Description>
      <Description>
        {undefinedUsers.length > 0 && (
          <>
            <span style={{ color: "var(--color-red-400)" }}>
              Undefined participants: {undefinedUsers.length}
            </span>
            <Button
              onClick={() =>
                download(
                  `undefined-participants-${contest.name}`,
                  undefinedUsers.join("\n"),
                )
              }
              size="small"
              variation="secondary"
            >
              Download
            </Button>
          </>
        )}
      </Description>
      <List onSubmit={handleSubmit(onSubmit)}>
        {contest.problems.map((item, index) => (
          <SubmissionItem key={index} item={item} index={index}>
            <>
              <strong>
                {item.index} (&quot;{item.name}&quot;)
              </strong>
              <ItemInput
                placeholder="Maximum points per task"
                data-index={index}
                error={errors[`${index}`]}
                disabled={isGetting}
                defaultValue={contestInfo[index.toString()] || null}
                {...register(`${index}`, {
                  required: "This field is required",
                  pattern: {
                    value: /^\d*\.?\d*$/,
                    message: "Incorrect value",
                  },
                  min: 0,
                })}
              />
              {errors[`${index}`] && (
                <Error>{errors[`${index}`].message}</Error>
              )}
            </>
          </SubmissionItem>
        ))}
        {/*errors?.total && <Error>{errors?.total?.message}</Error>*/}
        <SubmissionsSettings
          isGetting={isGetting}
          register={register}
          contestInfo={contestInfo}
          errors={errors}
          watch={watch}
        />
        <SourcesConfiguration
          contestID={info?.contest?.id}
          isGetting={isGetting}
          register={register}
          watch={watch}
          group={group}
        />
        {unpossibleReqest ? (
          <UndefinedDescription style={{ fontWeight: "400" }}>
            There are no solutions that could be obtained, please{" "}
            <b>wait for the end of the contest</b> or{" "}
            <Link to="/handles">download the handles</Link> of the participants
          </UndefinedDescription>
        ) : (
          <>
            <SubmissionsAction>
              <Controller
                control={control}
                name="selector"
                render={({ field }) => (
                  <Select
                    {...field}
                    placeholder="Choose submission type"
                    theme={selectTheme}
                    styles={selectStyles}
                    menuPosition="auto"
                    defaultValue={
                      options.find((el) => el?.value === "most points") ||
                      options[0]
                    }
                    options={options}
                  />
                )}
              />
              <Button disabled={isGetting} type="submit">
                {isGetting ? <SpinnerMini /> : "Create a rating file"}
              </Button>
            </SubmissionsAction>
            {selectedValue && (
              <SelectorDescription>
                {selectedValue?.description?.slice(0, 1).toUpperCase() +
                  selectedValue.description.slice(1)}
              </SelectorDescription>
            )}
          </>
        )}
      </List>
    </StyledCover>
  );
}

function SourcesConfiguration({
  contestID,
  register,
  isGetting,
  watch,
  group,
}) {
  const watchFileInput = watch("attempts");

  return (
    <LateSubmissionsContainer>
      <Heading as="h2">Attempts mapping</Heading>
      <SourcesDescription>
        In case you want to get attempts mapped to students emails, please add
        an archive of attempts, it can be obtained{" "}
        {group ? (
          <a
            href={`https://codeforces.com/group/${group}/contest/${contestID}/admin`}
            target="_blank"
          >
            by following the link
          </a>
        ) : (
          `by following the link: https://codeforces.com/group/${"<group-id>"}/contest/${contestID}/admin`
        )}
      </SourcesDescription>
      <FormElement
        label="Exported attemps"
        type="file"
        borderless={true}
        style={{ maxWidth: "34rem", marginLeft: "auto", marginRight: "auto" }}
      >
        <FileInput
          edited={watchFileInput && "true"}
          text={watchFileInput?.length ? watchFileInput[0]?.name : "*.zip"}
          accept={".zip"}
          register={register("attempts")}
          disabled={isGetting}
        />
      </FormElement>
    </LateSubmissionsContainer>
  );
}
function SubmissionsSettings({
  register,
  isGetting,
  contestInfo,
  errors,
  watch,
}) {
  const watchFileInput = watch("legal-exuses");

  return (
    <LateSubmissionsContainer>
      <Heading as="h2">Late Submission Configuration</Heading>
      <FormElement label="Legal excused students" type="file" borderless={true}>
        <FileInput
          edited={watchFileInput && "true"}
          text={watchFileInput?.length ? watchFileInput[0]?.name : "*.csv"}
          accept={".csv"}
          register={register("legal-exuses")}
          disabled={isGetting}
        />
      </FormElement>
      <Heading as="h3" style={{ gridColumn: "span 3" }}>
        Additional time for late submission
      </Heading>
      <TimeConfiguration>
        <FormElement label="Days" borderless={true}>
          <Input
            error={errors["additional-days"]}
            disabled={isGetting}
            placeholder={0}
            defaultValue={contestInfo["additional-days"] || null}
            {...register("additional-days", {
              min: 0,
            })}
            style={{ textAlign: "center" }}
          />
        </FormElement>
        <FormElement label="Hours" borderless={true}>
          <Input
            error={errors["additional-hours"]}
            disabled={isGetting}
            placeholder={0}
            defaultValue={contestInfo["additional-hours"] || null}
            {...register("additional-hours", {
              min: 0,
            })}
            style={{ textAlign: "center" }}
          />
        </FormElement>
        <FormElement label="Minutes" borderless={true}>
          <Input
            disabled={isGetting}
            placeholder={0}
            error={errors["additional-minutes"]}
            defaultValue={contestInfo["additional-minutes"] || null}
            {...register("additional-minutes", {
              min: 0,
            })}
            style={{ textAlign: "center" }}
          />
        </FormElement>
      </TimeConfiguration>
      <FormElement label="Penalty percentage" borderless={true}>
        <Input
          disabled={isGetting}
          placeholder={20}
          error={errors?.penalty}
          defaultValue={contestInfo["penalty"] || null}
          {...register("penalty", {
            min: {
              value: 0,
            },
            max: {
              value: 100,
            },
          })}
          style={{ textAlign: "center" }}
        />
      </FormElement>
    </LateSubmissionsContainer>
  );
}
function SubmissionItem({ item, children }) {
  return (
    <Item>
      {children}
      <ItemRow>
        <span>
          Total number of sumbissions:
          <strong>{item?.submissions?.length}</strong>
        </span>
      </ItemRow>
    </Item>
  );
}

export default SubmissionsInfo;
