<!--
鏂囦欢锛歝lawhub-copy.md
鏍稿績鍔熻兘锛氫綔涓?Fitness skill 鐨勬寮忓彂甯冮〉鏂囨锛屼緵 ClawHub / OpenClaw 鎴栧悓绫绘妧鑳藉競鍦虹洿鎺ュ鐢ㄣ€?杈撳叆锛欶itness 鍒嗘敮鐨?AKM 瀹氫綅銆佹柟娉曠粨鏋勩€佸閮ㄦ祴璇曠粨璁轰笌浣跨敤杈圭晫銆?杈撳嚭锛氬彲鐩存帴涓婄嚎鐨勬妧鑳介〉闀跨増鏂囨銆?-->

# AKM Fitness ClawHub Skill Page

## Skill Title

**AKM Fitness: Constraint-Aware Training Planner**

## One-line Description

Build the training profile first, then make workout decisions that respect body limits, equipment reality, recovery, and time budget.

## Install

```bash
npx skills add https://github.com/sirsws/akm --skill akm-fitness-planner --full-depth
``` 

## What It Is

Most fitness agents answer too early.

They assume the user has one clear goal, enough time, normal recovery, and a stable gym environment.
That is usually false.

AKM Fitness fixes this by forcing the system to model the operator first:

- goal priority
- body constraints
- equipment context
- time budget
- recovery state
- adherence risks

Only then does it make a training decision.

## What Makes It Different

This is not just a workout prompt.
It is a three-stage method:

1. elicitation
2. structured record
3. execution decision

The output is not generic programming language.
It is a constraint-aware training judgment.

## Best Fit

Use this skill when:

- injuries or physical limits materially affect training
- equipment availability changes the decision
- the user needs realistic planning under hard time limits
- generic plans keep failing in practice

## Boundary

- not a medical diagnosis tool
- not a rehab replacement
- not a bodybuilding template generator
- does not pretend missing critical inputs are known

## Closing Line

**No profile, no serious plan.**