package utils

import (
	"fmt"
	"regexp"

	"github.com/go-playground/validator/v10"
)

var (
	validate *validator.Validate

	hashtagRegex = regexp.MustCompile(`^[a-zA-Z/]{1,15}$`)
	companyRegex = regexp.MustCompile(`^[a-zA-Z가-힣0-9]{1,10}$`)
	queryRegex   = regexp.MustCompile(`^[가-힣a-zA-Z0-9\s/,&+]{1,15}$`)
)

func init() {
	validate = validator.New()

	validate.RegisterValidation("hashtag", validateHashtag)
	validate.RegisterValidation("company", validateCompany)
	validate.RegisterValidation("query", validateQuery)
}

type SearchParams struct {
	Hashtags []string `validate:"omitempty,dive,hashtag,max=10"`
	Company  string   `validate:"omitempty,company"`
	Query    string   `validate:"omitempty,query"`
	Page     int      `validate:"min=0"`
	Size     int      `validate:"min=1,max=30"`
}

func ValidateParams(params SearchParams) error {
	if err := validate.Struct(params); err != nil {
		if _, ok := err.(*validator.InvalidValidationError); ok {
			return fmt.Errorf("invalid validation error")
		}

		for _, err := range err.(validator.ValidationErrors) {
			switch err.Field() {
			case "Hashtags":
				return fmt.Errorf("invalid hashtag: must be 1-15 characters, only letters and '/'")
			case "Company":
				return fmt.Errorf("invalid company name: must be 1-10 characters, only letters, numbers, and Korean characters")
			case "Query":
				return fmt.Errorf("invalid query: must be 1-15 characters, only letters, numbers, Korean characters, and spaces")
			case "Page":
				return fmt.Errorf("invalid page number: must be non-negative")
			case "Size":
				return fmt.Errorf("invalid page size: must be between 1 and 30")
			}
		}
	}

	return nil
}

func validateHashtag(fl validator.FieldLevel) bool {
	return hashtagRegex.MatchString(fl.Field().String())
}

func validateCompany(fl validator.FieldLevel) bool {
	return companyRegex.MatchString(fl.Field().String())
}

func validateQuery(fl validator.FieldLevel) bool {
	return queryRegex.MatchString(fl.Field().String())
}
